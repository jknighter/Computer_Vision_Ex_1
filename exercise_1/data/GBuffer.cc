// glow OpenGL wrapper
#include <glow/common/log.hh>
#include <glow/common/scoped_gl.hh>
#include <glow/objects/ArrayBuffer.hh>
#include <glow/objects/Framebuffer.hh>
#include <glow/objects/Program.hh>
#include <glow/objects/Texture2D.hh>
#include <glow/objects/TextureRectangle.hh>
#include <glow/objects/VertexArray.hh>

#include "GBuffer.hh"
void GBuffer::init() {
    mFramebuffer = glow::Framebuffer::create("fColor", mGBuffers); // Problem
    auto fb = mFramebuffer->bind();
}

// Render geometry data into G-Buffer
glow::UsedProgram GBuffer::renderToGBuffer()
{
    mGBufferPosition = glow::TextureRectangle::create(1, 1, GL_RGB16F);
    mGBufferNormal = glow::TextureRectangle::create(1, 1, GL_RGB16F);

    mFramebuffer = glow::Framebuffer::create("fColor", mGBufferNormal); //Problem
    auto fb = mFramebuffer->bind();
    GLOW_SCOPED(enable, GL_DEPTH_TEST);
    GLOW_SCOPED(enable, GL_CULL_FACE);

    mShaderGBuffer = glow::Program::createFromFile("../data/shaders/gbuffer");
    auto shader = mShaderGBuffer->use();

    return shader;
}

// Read data from G-Buffer
void GBuffer::readFromGBuffer(glow::UsedProgram shader) {}